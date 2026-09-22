<?php
/**
 * Writer's Desk theme functions.
 * This theme changes presentation only.
 */
function writers_desk_setup() {
    add_theme_support( 'title-tag' );
    add_theme_support( 'post-thumbnails' );
    add_theme_support( 'custom-logo' );
    add_theme_support( 'html5', array( 'search-form', 'comment-form', 'comment-list', 'gallery', 'caption' ) );
}
add_action( 'after_setup_theme', 'writers_desk_setup' );

function writers_desk_assets() {
    wp_enqueue_style( 'writers-desk', get_template_directory_uri() . '/assets/theme.css', array(), '1.0.0' );
    wp_enqueue_script( 'writers-desk', get_template_directory_uri() . '/assets/theme.js', array(), '1.0.0', true );
}
add_action( 'wp_enqueue_scripts', 'writers_desk_assets' );

function writers_desk_body_classes( $classes ) {
    $profile = get_theme_mod( 'writers_desk_profile', 'writer' );
    $classes[] = 'profile-' . sanitize_html_class( $profile );
    return $classes;
}
add_filter( 'body_class', 'writers_desk_body_classes' );

function writers_desk_customize_register( $wp_customize ) {
    $wp_customize->add_section( 'writers_desk_options', array(
        'title' => __( 'Writer Desk options', 'writers-desk' ),
        'priority' => 30,
        'description' => __( 'Optional tools stay off until enabled.', 'writers-desk' ),
    ) );
    $wp_customize->add_setting( 'writers_desk_profile', array( 'default' => 'writer', 'sanitize_callback' => 'sanitize_key' ) );
    $wp_customize->add_control( 'writers_desk_profile', array(
        'section' => 'writers_desk_options', 'label' => __( 'Reading profile', 'writers-desk' ), 'type' => 'select',
        'choices' => array( 'writer' => __( 'Writer', 'writers-desk' ), 'source' => __( 'Source Notes', 'writers-desk' ), 'large' => __( 'Large Type', 'writers-desk' ) ),
    ) );
    foreach ( array( 'writers_desk_enable_banner' => __( 'Show the banner maker link', 'writers-desk' ), 'writers_desk_enable_activities' => __( 'Show the optional activities link', 'writers-desk' ) ) as $setting => $label ) {
        $wp_customize->add_setting( $setting, array( 'default' => false, 'sanitize_callback' => 'rest_sanitize_boolean' ) );
        $wp_customize->add_control( $setting, array( 'section' => 'writers_desk_options', 'label' => $label, 'type' => 'checkbox' ) );
    }
}
add_action( 'customize_register', 'writers_desk_customize_register' );
