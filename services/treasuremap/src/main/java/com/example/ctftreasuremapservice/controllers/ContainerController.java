package com.example.ctftreasuremapservice.controllers;


import com.example.ctftreasuremapservice.manager.ContainerManager;
import com.example.ctftreasuremapservice.model.dto.ContainerDto;
import com.example.ctftreasuremapservice.utils.Utils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDate;

@RestController
public class ContainerController {

    private final ContainerManager containerManager;
    private final Logger logger = LoggerFactory.getLogger("container-controller");

    public ContainerController(ContainerManager containerManager) {
        this.containerManager = containerManager;
    }

    @PostMapping("/container/save")
    public void saveContainerToLocation(@RequestBody ContainerDto containerDto) {
        try {
            containerManager.saveContainer(containerDto.getTreasure(), containerDto.getLocationName());
        } catch (Exception e) {
            logger.error("[" + LocalDate.now() + "]" + "[ERROR] from " + Utils.getRequestRemoteAddr() + " with username = " + SecurityContextHolder.getContext().getAuthentication().getPrincipal() + " /container/save > [MainController] [ERROR]");
        }
        logger.info("[" + LocalDate.now() + "]" + "[INFO] from " + Utils.getRequestRemoteAddr() + " with username = " + SecurityContextHolder.getContext().getAuthentication().getPrincipal() + " /container/save > [MainController] [SUCCESS]");
    }
}
