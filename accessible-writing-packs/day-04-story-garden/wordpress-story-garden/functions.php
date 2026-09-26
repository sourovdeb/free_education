<?php
/**
 * Story Garden theme functions.
 * This theme changes presentation only.
 */
function story_garden_setup() {
    add_theme_support( 'title-tag' );
    add_theme_support( 'post-thumbnails' );
    add_theme_support( 'custom-logo' );
    add_theme_support( 'html5', array( 'search-form', 'comment-form', 'comment-list', 'gallery', 'caption' ) );
}
add_action( 'after_setup_theme', 'story_garden_setup' );

function story_garden_assets() {
    wp_enqueue_style( 'story-garden', get_template_directory_uri() . '/assets/theme.css', array(), '1.0.0' );
    wp_enqueue_script( 'story-garden', get_template_directory_uri() . '/assets/theme.js', array(), '1.0.0', true );
}
add_action( 'wp_enqueue_scripts', 'story_garden_assets' );

function story_garden_body_classes( $classes ) {
    $profile = get_theme_mod( 'story_garden_profile', 'writer' );
    $classes[] = 'profile-' . sanitize_html_class( $profile );
    return $classes;
}
add_filter( 'body_class', 'story_garden_body_classes' );

function story_garden_sanitize_profile( $value ) {
    $allowed = array( 'writer', 'source', 'large' );
    return in_array( $value, $allowed, true ) ? $value : 'writer';
}

function story_garden_customize_register( $wp_customize ) {
    $wp_customize->add_section( 'story_garden_options', array(
        'title' => __( 'Story Garden options', 'story-garden' ),
        'priority' => 30,
        'description' => __( 'Optional tools stay off until enabled.', 'story-garden' ),
    ) );
    $wp_customize->add_setting( 'story_garden_profile', array( 'default' => 'writer', 'sanitize_callback' => 'story_garden_sanitize_profile' ) );
    $wp_customize->add_control( 'story_garden_profile', array(
        'section' => 'story_garden_options', 'label' => __( 'Reading profile', 'story-garden' ), 'type' => 'select',
        'choices' => array( 'writer' => __( 'Writer', 'story-garden' ), 'source' => __( 'Source Notes', 'story-garden' ), 'large' => __( 'Large Type', 'story-garden' ) ),
    ) );
    foreach ( array( 'story_garden_enable_banner' => __( 'Show the banner maker link', 'story-garden' ), 'story_garden_enable_activities' => __( 'Show the optional activities link', 'story-garden' ) ) as $setting => $label ) {
        $wp_customize->add_setting( $setting, array( 'default' => false, 'sanitize_callback' => 'rest_sanitize_boolean' ) );
        $wp_customize->add_control( $setting, array( 'section' => 'story_garden_options', 'label' => $label, 'type' => 'checkbox' ) );
    }
}
add_action( 'customize_register', 'story_garden_customize_register' );
