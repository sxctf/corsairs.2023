package com.example.ctftreasuremapservice.model.pojo;

import lombok.Getter;
import lombok.Setter;

import java.util.UUID;


@Getter
@Setter
public class Container {
    private UUID id;
    private String treasure;
    private String author;

    public Container(String treasure, String author) {
        this.id = UUID.randomUUID();
        this.treasure = treasure;
        this.author = author;
    }
}
