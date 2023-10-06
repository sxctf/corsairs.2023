package com.example.ctftreasuremapservice.security;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.session.HttpSessionEventPublisher;


@Configuration
@EnableWebSecurity
public class SecurityConfiguration {

    private final AuthenticationService authenticationService;

    public SecurityConfiguration(AuthenticationService authenticationService) {
        this.authenticationService = authenticationService;
    }


    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http.authorizeHttpRequests(request -> {
                    request.requestMatchers("/").permitAll();
                    request.requestMatchers("/js/**").permitAll();
                    request.requestMatchers("/login").permitAll();
                    request.requestMatchers("/registration/fragment").permitAll();
                    request.requestMatchers("/auth-page/fragment").permitAll();
                    request.requestMatchers("/location/data/**").permitAll();
                    request.requestMatchers("/styles/**").permitAll();
                    request.requestMatchers("/image/**").permitAll();
                    request.requestMatchers("/auth-page").permitAll();
                    request.requestMatchers("/registration").permitAll();
                    request.requestMatchers("/user/create").permitAll();
                    request.requestMatchers("/container/save").permitAll();
                    request.anyRequest().authenticated();
                })
                .formLogin((httpSecurityFormLoginConfigurer ->
                {
                    httpSecurityFormLoginConfigurer.loginPage("/auth-page");
                    httpSecurityFormLoginConfigurer.defaultSuccessUrl("/main-page");
                    httpSecurityFormLoginConfigurer.loginProcessingUrl("/login").permitAll();
                }))
                .csrf((AbstractHttpConfigurer::disable))
                .authenticationProvider(authenticationService)
                .sessionManagement((httpSecuritySessionManagementConfigurer -> {
                    httpSecuritySessionManagementConfigurer.sessionCreationPolicy(SessionCreationPolicy.IF_REQUIRED);
                    httpSecuritySessionManagementConfigurer.sessionFixation().migrateSession();
                }));

        return http.build();
    }


    @Bean
    public HttpSessionEventPublisher httpSessionEventPublisher() {
        return new HttpSessionEventPublisher();
    }


}