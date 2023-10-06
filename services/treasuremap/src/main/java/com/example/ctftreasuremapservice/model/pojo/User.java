package com.example.ctftreasuremapservice.model.pojo;


import lombok.Builder;
import lombok.Getter;
import lombok.Setter;

import java.util.UUID;

@Getter
@Setter
@Builder
public class User {
    private UUID id;
    private String username;
    private String password;
}
