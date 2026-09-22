<!doctype html>
<html <?php language_attributes(); ?>>
<head>
<meta charset="<?php bloginfo( 'charset' ); ?>">
<meta name="viewport" content="width=device-width, initial-scale=1">
<?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>
<a class="skip-link" href="#main"><?php esc_html_e( 'Skip to writing', 'writers-desk' ); ?></a>
<header class="site-header">
  <div>
    <p class="eyebrow">WRITER'S DESK / <?php echo esc_html( strtoupper( get_theme_mod( 'writers_desk_profile', 'writer' ) ) ); ?></p>
    <?php if ( has_custom_logo() ) { the_custom_logo(); } ?>
    <a class="site-title" href="<?php echo esc_url( home_url( '/' ) ); ?>"><?php bloginfo( 'name' ); ?></a>
  </div>
  <button class="settings-toggle" type="button" aria-expanded="false" aria-controls="reading-settings">Reading settings</button>
</header>
<aside id="reading-settings" class="reading-settings" hidden>
  <label>Text size <input type="range" min="100" max="150" value="100" data-font-scale></label>
  <label><input type="checkbox" data-contrast> High contrast</label>
  <label><input type="checkbox" data-motion> Reduce motion</label>
</aside>
