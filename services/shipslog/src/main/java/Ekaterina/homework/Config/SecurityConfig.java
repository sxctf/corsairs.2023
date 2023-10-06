package Ekaterina.homework.Config;


import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.www.BasicAuthenticationEntryPoint;
import org.springframework.security.web.context.HttpSessionSecurityContextRepository;

@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public PasswordEncoder passwordEncoder()
    {
        return new BCryptPasswordEncoder();
    }

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        var realmName = "localhost";
        var entryPoint= new BasicAuthenticationEntryPoint();
        entryPoint.setRealmName(realmName);

        return http
                .httpBasic(httpBasic -> httpBasic
                        .realmName(realmName)
                        .authenticationEntryPoint(entryPoint)
                        .securityContextRepository(
                                // Хранение контекста безопасности в HTTP-сессии
                                new HttpSessionSecurityContextRepository()))
                // Создание HTTP-сессии при необходимости
                .sessionManagement(sessionManagement -> sessionManagement
                        .sessionCreationPolicy(SessionCreationPolicy.ALWAYS))
                .authorizeHttpRequests(authorizedRequests -> authorizedRequests
                        .requestMatchers("/private-news", "/check", "/news", "/index", "/verification-code", "/add", "/checkCode")
                        .permitAll().anyRequest().anonymous()
                        )
                .csrf().disable()
                .build();

    }



}

