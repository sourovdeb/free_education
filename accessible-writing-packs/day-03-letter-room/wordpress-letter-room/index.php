<?php get_header(); ?>
<main id="main" class="writing-flow">
<?php if ( have_posts() ) : while ( have_posts() ) : the_post(); ?>
  <article <?php post_class( 'letter-card' ); ?>>
    <div class="letter-meta"><span><?php echo esc_html( get_the_date() ); ?></span><span><?php the_category( ', ' ); ?></span></div>
    <h1><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h1>
    <div class="entry-copy"><?php the_excerpt(); ?></div>
    <a class="read-link" href="<?php the_permalink(); ?>">Open letter</a>
  </article>
<?php endwhile; the_posts_navigation(); else : ?>
  <article><h1>Nothing published yet.</h1><p>Start a post when ready.</p></article>
<?php endif; ?>
</main>
<?php get_footer(); ?>
