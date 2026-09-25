"""Tests use mocks, never paid APIs."""
import copy, importlib.util, json, os, subprocess, sys, tempfile, time, unittest
from pathlib import Path
from unittest.mock import patch
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE))
import director as d


def response(template='steps',motion='still',support=1,confidence=.95,facts=0):
    answers={}
    for name,choice in [('template',template),('motion',motion)]:
        answers[name]={'type':'choice','choice':choice,'confidence':confidence,
                       'probabilities':{key:float(key==choice) for key in d.QUESTIONS[name]['criteria']}}
    answers.update(supported={'type':'noul','noul':support},fact_check={'type':'noul','noul':facts})
    return {'model':'TEST-FIXTURE-NOT-A-LIVE-MODEL','answers':answers}


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)
        self.source=self.root/'test.srt'
        self.source.write_text('1\n00:00:01,000 --> 00:00:09,000\nRead the question. Think about it. Write your answer.\n\n2\n00:00:10,000 --> 00:00:18,000\nTeam A has 10 books. Team B has 20 books.\n',encoding='utf-8')
        # Tests allow non-E temporary roots.
        self.root_patch=patch.object(d,'root_path',side_effect=self.local_root)
        self.root_patch.start()
        self.env_patch=patch.dict(os.environ,{},clear=False);self.env_patch.start()
        self.project=d.ingest(self.source,self.root,'test','25','Test timeline')
        self.meta=d.load(self.project/'project.json')
        self.visual={'id':'v001','source_ids':['s0001'],'evidence':'Read the question. Think about it. Write your answer.',
                     'template':'steps','mode':'still','start':1,'end':9,'title':'Answering a question','labels':['Read','Think','Write']}
        self.proposal={'source_sha256':self.meta['source_sha256'],'visuals':[self.visual]}
        d.save(self.project/'01_work/proposal.json',self.proposal)
    def tearDown(self):
        self.env_patch.stop();self.root_patch.stop();self.tmp.cleanup()
    def local_root(self,root):
        path=Path(root).resolve();path.mkdir(parents=True,exist_ok=True);return path
    def validate(self,proposal=None):
        return d.validate_proposal(proposal or self.proposal,d.load(self.project/'01_work/transcript.json'),self.meta,self.project)
    def mock_evaluate(self,answer=None):
        with patch.object(d,'ask_typesafe',return_value=(answer or response(),{'cache_hit':False,'request_id':None,'response_sha256':'test'})):
            return d.evaluate(self.project,True)
    def test_srt_and_ids(self):
        t=d.parse_transcript(self.source);self.assertEqual(t['segments'][1]['id'],'s0002');self.assertEqual(t['segments'][0]['start'],1)
    def test_fractional_rate(self):
        p=d.ingest(self.source,self.root,'fractional','29.97','Timeline')
        self.assertEqual(d.load(p/'project.json')['fps'],'30000/1001')
    def test_transcript_offset(self):
        p=d.ingest(self.source,self.root,'offset','25','Timeline',1)
        self.assertEqual(d.load(p/'01_work/transcript.json')['segments'][0]['start'],0)
    def test_offset_rejects_negative_placement(self):
        with self.assertRaises(d.Stop):d.ingest(self.source,self.root,'bad-offset','25','Timeline',2)
    def test_vtt(self):
        p=self.root/'test.vtt';p.write_text('WEBVTT\n\n00:01.000 --> 00:04.000 align:start\nHello.\n')
        self.assertEqual(d.parse_transcript(p)['segments'][0]['text'],'Hello.')
    def test_whisper_json(self):
        p=self.root/'t.json';d.save(p,{'segments':[{'start':0,'end':4,'text':'Hello'}]})
        self.assertEqual(len(d.parse_transcript(p)['segments']),1)
    def test_untimed_blocked(self):
        p=self.root/'t.txt';p.write_text('No timestamps')
        with self.assertRaises(d.Stop):d.parse_transcript(p)
    def test_bad_timestamp(self):
        with self.assertRaises(d.Stop):d.stamp('00:00:61')
    def test_valid_proposal(self):self.assertEqual(len(self.validate()),1)
    def test_invented_number_blocked(self):
        self.visual['title']='Answer in 40 steps'
        with self.assertRaises(d.Stop):self.validate()
    def test_wrong_quote_blocked(self):
        self.visual['evidence']='Never spoken'
        with self.assertRaises(d.Stop):self.validate()
    def test_unknown_source_blocked(self):
        self.visual['source_ids']=['s9999']
        with self.assertRaises(d.Stop):self.validate()
    def test_nan_blocked(self):
        self.visual['start']=float('nan')
        with self.assertRaises(d.Stop):self.validate()
    def test_external_path_blocked(self):
        with self.assertRaises(d.Stop):d.inside(self.project,self.root/'secret')
    def test_source_mutation_blocked(self):
        (self.project/self.meta['source_path']).write_text('Changed')
        with self.assertRaises(d.Stop):d.project_path(self.project)
    def test_transcript_mutation_blocked(self):
        d.save(self.project/'01_work/transcript.json',{'segments':[]})
        with self.assertRaises(d.Stop):d.project_path(self.project)
    def test_unsupported_template(self):
        self.visual['template']='execute_shell'
        with self.assertRaises(d.Stop):self.validate()
    def test_number_evidence(self):
        self.visual.update(source_ids=['s0002'],evidence='Team A has 10 books. Team B has 20 books.',template='bars',start=10,end=18,title='Books',labels=['Team A','Team B'],values=[10,20],unit='books')
        self.assertEqual(len(self.validate()),1)
    def test_typeguard(self):
        self.assertEqual(d.check_answer(response())['template']['choice'],'steps')
    def test_boolean_confidence_rejected(self):
        r=response();r['answers']['template']['confidence']=True
        with self.assertRaises(d.Stop):d.check_answer(r)
    def test_missing_probability_rejected(self):
        r=response();r['answers']['template']['probabilities'].pop('quote')
        with self.assertRaises(d.Stop):d.check_answer(r)
    def test_low_confidence_review(self):
        self.assertEqual(d.classify(self.visual,response(confidence=.1))[0],'REVIEW')
    def test_unsupported_content_review(self):
        self.assertEqual(d.classify(self.visual,response(support=.2))[0],'REVIEW')
    def test_fact_check_review(self):
        self.assertEqual(d.classify(self.visual,response(facts=1))[0],'REVIEW')
    def test_skip_routing(self):
        self.assertEqual(d.classify(self.visual,response(motion='skip'))[0],'SKIP')
    def test_offline_cannot_approve(self):
        plan=d.evaluate(self.project,False);self.assertEqual(plan['items'][0]['status'],'UNVERIFIED')
        with self.assertRaises(d.Stop):d.approve(self.project,True)
    def test_review_is_required(self):
        self.mock_evaluate()
        with self.assertRaises(d.Stop):d.approve(self.project,False)
    def test_stale_proposal_blocked(self):
        self.mock_evaluate();d.approve(self.project,True)
        self.visual['title']='A changed title';d.save(self.project/'01_work/proposal.json',self.proposal)
        with self.assertRaises(d.Stop):d.plan_checked(self.project)
    def test_type_safe_cache(self):
        state={'test':'fixture'}
        payload={'model':d.POLICY['model'],'state':state,'questions':d.QUESTIONS}
        key=d.digest({'request':payload,'policy':d.POLICY})
        d.save(self.root/'cache/typesafe'/f'{key}.json',{'created':time.time(),'request_id':None,'response':response()})
        result,receipt=d.ask_typesafe(state,self.root,self.project)
        self.assertTrue(receipt['cache_hit']);self.assertIsNone(receipt['request_id'])
    def test_budget_blocks_without_network(self):
        d.save(self.project/'01_work/typesafe_budget.json',{'attempts':d.POLICY['max_requests_per_project']})
        with patch.dict(os.environ,{'TYPESAFE_API_KEY':'test-not-a-real-key'}):
            with self.assertRaises(d.Stop):d.ask_typesafe({'fresh':True},self.root,self.project)
    def test_html_escapes_text(self):
        self.visual['title']='<script>alert</script>';d.save(self.project/'01_work/proposal.json',self.proposal)
        d.evaluate(self.project,False)
        page=(self.project/'01_work/review.html').read_text();self.assertNotIn('<script>',page)
    @unittest.skipUnless(importlib.util.find_spec('PIL'),'Pillow is needed')
    def test_still_renderer(self):
        import still
        p=self.root/'poster.png';still.render(self.visual,p)
        self.assertEqual(d.verify_asset(p,self.visual,'25')['format'],'png')
    @unittest.skipUnless(importlib.util.find_spec('PIL') and importlib.util.find_spec('psutil'),'Render dependencies are needed')
    def test_still_pipeline_with_mock_typesafe(self):
        self.mock_evaluate();d.approve(self.project,True)
        with patch.object(d,'guard_resources',return_value=None):
            manifest=d.render(self.project)
        self.assertEqual(len(manifest['assets']),1)
        self.assertTrue(Path(manifest['assets'][0]['path']).exists())
        self.assertEqual(manifest['assets'][0]['start_frame'],25)
        completed=subprocess.run([sys.executable,str(BASE/'resolve_import.py'),'--manifest',str(self.project/'02_resolve/manifest.json')],capture_output=True,text=True)
        self.assertEqual(completed.returncode,0,completed.stderr)
        self.assertIn('dry_run',completed.stdout)

if __name__=='__main__':unittest.main()
