package com.example.ctftreasuremapservice.entity;

import jakarta.persistence.*;
import lombok.Getter;

import java.util.UUID;

@Getter
@Entity
public class ContainerEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private UUID id;
    private String treasure;
    private String author;
    @ManyToOne
    private LocationEntity locationEntity;

    public ContainerEntity() {
    }

    public ContainerEntity(String treasure, String author, LocationEntity locationEntity) {
        this.id = UUID.randomUUID();
        this.treasure = treasure;
        this.author = author;
        this.locationEntity = locationEntity;
    }
}
