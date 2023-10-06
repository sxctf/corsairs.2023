package com.example.ctftreasuremapservice.controllers;

import com.example.ctftreasuremapservice.manager.ContainerManager;
import com.example.ctftreasuremapservice.utils.Utils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.ModelAndView;

import java.time.LocalDate;

@RestController
public class LocationController {

    private final ContainerManager containerManager;
    private final Logger logger = LoggerFactory.getLogger("location-controller");

    public LocationController(ContainerManager containerManager) {
        this.containerManager = containerManager;
    }

    @GetMapping("/location/data/{locationName}")
    public ModelAndView getLocationData(@PathVariable String locationName) {
        ModelAndView model = new ModelAndView("location-data-fragment.html");
        try {
            model.addObject("containers", containerManager.getContainersByLocationName(locationName));
        } catch (Exception e) {
            logger.error("[" + LocalDate.now() + "]" + "[ERROR] from " + Utils.getRequestRemoteAddr() + " with username = " + SecurityContextHolder.getContext().getAuthentication().getPrincipal() + " /location/data/{locationName} > [MainController] [ERROR]");
        }
        logger.info("[" + LocalDate.now() + "]" + "[INFO] from " + Utils.getRequestRemoteAddr() + " with username = " + SecurityContextHolder.getContext().getAuthentication().getPrincipal() + " /location/data/{locationName} > [MainController] [SUCCESS]");

        return model;
    }
}
