<?php
/**
 * Letter Room theme functions.
 * This theme changes presentation only.
 */
function letter_room_setup() {
    add_theme_support( 'title-tag' );
    add_theme_support( 'post-thumbnails' );
    add_theme_support( 'custom-logo' );
    add_theme_support( 'html5', array( 'search-form', 'comment-form', 'comment-list', 'gallery', 'caption' ) );
}
add_action( 'after_setup_theme', 'letter_room_setup' );

function letter_room_assets() {
    wp_enqueue_style( 'letter-room', get_template_directory_uri() . '/assets/theme.css', array(), '1.0.0' );
    wp_enqueue_script( 'letter-room', get_template_directory_uri() . '/assets/theme.js', array(), '1.0.0', true );
}
add_action( 'wp_enqueue_scripts', 'letter_room_assets' );

function letter_room_body_classes( $classes ) {
    $profile = get_theme_mod( 'letter_room_profile', 'large' );
    $classes[] = 'profile-' . sanitize_html_class( $profile );
    return $classes;
}
add_filter( 'body_class', 'letter_room_body_classes' );

function letter_room_sanitize_profile( $value ) {
    $allowed = array( 'writer', 'source', 'large' );
    return in_array( $value, $allowed, true ) ? $value : 'large';
}

function letter_room_customize_register( $wp_customize ) {
    $wp_customize->add_section( 'letter_room_options', array(
        'title' => __( 'Letter Room options', 'letter-room' ),
        'priority' => 30,
        'description' => __( 'Optional tools stay off until enabled.', 'letter-room' ),
    ) );
    $wp_customize->add_setting( 'letter_room_profile', array( 'default' => 'large', 'sanitize_callback' => 'letter_room_sanitize_profile' ) );
    $wp_customize->add_control( 'letter_room_profile', array(
        'section' => 'letter_room_options', 'label' => __( 'Reading profile', 'letter-room' ), 'type' => 'select',
        'choices' => array( 'writer' => __( 'Writer', 'letter-room' ), 'source' => __( 'Source Notes', 'letter-room' ), 'large' => __( 'Large Type', 'letter-room' ) ),
    ) );
    foreach ( array( 'letter_room_enable_banner' => __( 'Show the banner maker link', 'letter-room' ), 'letter_room_enable_activities' => __( 'Show the optional activities link', 'letter-room' ) ) as $setting => $label ) {
        $wp_customize->add_setting( $setting, array( 'default' => false, 'sanitize_callback' => 'rest_sanitize_boolean' ) );
        $wp_customize->add_control( $setting, array( 'section' => 'letter_room_options', 'label' => $label, 'type' => 'checkbox' ) );
    }
}
add_action( 'customize_register', 'letter_room_customize_register' );
