<?php
/**
 * Template Name: Optional Activities
 */
get_header();
?>
<main id="main" class="writing-flow">
  <article>
    <p class="eyebrow">OPTIONAL / SELF-PACED</p>
    <h1><?php the_title(); ?></h1>
    <?php if ( get_theme_mod( 'letter_room_enable_activities', false ) ) : ?>
      <p>These activities are optional. They collect no information and make no treatment claim.</p>
      <p><a class="read-link" href="<?php echo esc_url( get_template_directory_uri() . '/activities/index.html' ); ?>">Open activities</a></p>
    <?php else : ?>
      <p>Activities are installed but off. Enable them in Appearance then Customize then Letter Room options.</p>
    <?php endif; ?>
  </article>
</main>
<?php get_footer(); ?>
