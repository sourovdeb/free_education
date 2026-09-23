<?php
/**
 * Source Notebook theme functions.
 * This theme changes presentation only.
 */
function source_notebook_setup() {
    add_theme_support( 'title-tag' );
    add_theme_support( 'post-thumbnails' );
    add_theme_support( 'custom-logo' );
    add_theme_support( 'html5', array( 'search-form', 'comment-form', 'comment-list', 'gallery', 'caption' ) );
}
add_action( 'after_setup_theme', 'source_notebook_setup' );

function source_notebook_assets() {
    wp_enqueue_style( 'source-notebook', get_template_directory_uri() . '/assets/theme.css', array(), '1.0.0' );
    wp_enqueue_script( 'source-notebook', get_template_directory_uri() . '/assets/theme.js', array(), '1.0.0', true );
}
add_action( 'wp_enqueue_scripts', 'source_notebook_assets' );

function source_notebook_body_classes( $classes ) {
    $profile = get_theme_mod( 'source_notebook_profile', 'source' );
    $classes[] = 'profile-' . sanitize_html_class( $profile );
    return $classes;
}
add_filter( 'body_class', 'source_notebook_body_classes' );

function source_notebook_sanitize_profile( $value ) {
    $allowed = array( 'writer', 'source', 'large' );
    return in_array( $value, $allowed, true ) ? $value : 'source';
}

function source_notebook_customize_register( $wp_customize ) {
    $wp_customize->add_section( 'source_notebook_options', array(
        'title' => __( 'Source Notebook options', 'source-notebook' ),
        'priority' => 30,
        'description' => __( 'Optional tools stay off until enabled.', 'source-notebook' ),
    ) );
    $wp_customize->add_setting( 'source_notebook_profile', array( 'default' => 'source', 'sanitize_callback' => 'source_notebook_sanitize_profile' ) );
    $wp_customize->add_control( 'source_notebook_profile', array(
        'section' => 'source_notebook_options', 'label' => __( 'Reading profile', 'source-notebook' ), 'type' => 'select',
        'choices' => array( 'writer' => __( 'Writer', 'source-notebook' ), 'source' => __( 'Source Notes', 'source-notebook' ), 'large' => __( 'Large Type', 'source-notebook' ) ),
    ) );
    foreach ( array( 'source_notebook_enable_banner' => __( 'Show the banner maker link', 'source-notebook' ), 'source_notebook_enable_activities' => __( 'Show the optional activities link', 'source-notebook' ) ) as $setting => $label ) {
        $wp_customize->add_setting( $setting, array( 'default' => false, 'sanitize_callback' => 'rest_sanitize_boolean' ) );
        $wp_customize->add_control( $setting, array( 'section' => 'source_notebook_options', 'label' => $label, 'type' => 'checkbox' ) );
    }
}
add_action( 'customize_register', 'source_notebook_customize_register' );
