package com.example.ctftreasuremapservice.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.util.UUID;


@Table(name = "user_table")
@Entity
@Getter
@Setter
public class UserEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private UUID id;
    private String username;
    private String password;
    private boolean isAdmin;

    public UserEntity(UUID id, String name, String password) {
        this.id = id;
        this.username = name;
        this.password = password;
        this.isAdmin = false;
    }

    public UserEntity() {
    }
}