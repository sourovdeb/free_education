<?php get_header(); ?>
<main id="main" class="writing-flow">
<?php while ( have_posts() ) : the_post(); ?>
  <article class="notebook-page">
    <p class="eyebrow">REFERENCE PAGE</p>
    <h1><?php the_title(); ?></h1>
    <div class="entry-copy"><?php the_content(); ?></div>
  </article>
<?php endwhile; ?>
</main>
<?php get_footer(); ?>
