<footer class="site-footer">
  <p>Letter Room stays tracker-free.</p>
  <?php if ( get_theme_mod( 'letter_room_enable_banner', false ) ) : ?>
    <a href="<?php echo esc_url( get_template_directory_uri() . '/tools/banner-maker/index.html' ); ?>">Open banner maker</a>
  <?php endif; ?>
  <?php if ( get_theme_mod( 'letter_room_enable_activities', false ) ) : ?>
    <a href="<?php echo esc_url( get_template_directory_uri() . '/activities/index.html' ); ?>">Open optional activities</a>
  <?php endif; ?>
</footer>
<?php wp_footer(); ?>
</body>
</html>
