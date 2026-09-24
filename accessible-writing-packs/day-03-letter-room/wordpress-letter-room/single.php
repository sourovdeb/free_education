<?php get_header(); ?>
<main id="main" class="writing-flow">
<?php while ( have_posts() ) : the_post(); ?>
  <article class="letter-page">
    <div class="letter-meta"><span><?php echo esc_html( get_the_date() ); ?></span><span><?php the_category( ', ' ); ?></span></div>
    <h1><?php the_title(); ?></h1>
    <div class="entry-copy"><?php the_content(); ?></div>
    <nav class="letter-navigation" aria-label="Adjacent writing"><?php the_post_navigation(); ?></nav>
  </article>
<?php endwhile; ?>
</main>
<?php get_footer(); ?>
