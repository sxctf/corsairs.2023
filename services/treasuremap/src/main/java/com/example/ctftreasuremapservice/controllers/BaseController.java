package com.example.ctftreasuremapservice.controllers;


import com.example.ctftreasuremapservice.entity.LocationEntity;
import com.example.ctftreasuremapservice.exception.UserAlreadyExistException;
import com.example.ctftreasuremapservice.manager.ContainerManager;
import com.example.ctftreasuremapservice.manager.LocationManager;
import com.example.ctftreasuremapservice.manager.UserManager;
import com.example.ctftreasuremapservice.model.dto.UserDto;
import com.example.ctftreasuremapservice.model.pojo.User;
import com.example.ctftreasuremapservice.utils.Utils;
import jakarta.servlet.ServletContext;
import org.apache.commons.io.IOUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.http.HttpStatusCode;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.ModelAndView;
import org.springframework.web.servlet.view.RedirectView;

import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.time.LocalDate;
import java.util.List;

@RestController
public class BaseController {
    private final ContainerManager containerManager;
    private final LocationManager locationManager;
    private final UserManager userManager;
    private final Logger logger = LoggerFactory.getLogger("base-controller");

    @Autowired
    public BaseController(ContainerManager containerManager,
                          LocationManager locationManager,
                          UserManager userManager) {
        this.containerManager = containerManager;
        this.locationManager = locationManager;
        this.userManager = userManager;
    }

    @GetMapping("/")
    public ModelAndView getDefaultPage() {
        ModelAndView modelAndView;
        if (!userManager.isAdmin()) {
            modelAndView = new ModelAndView("main-page-non-authorized.html");
        } else {
            return new ModelAndView(new RedirectView("/main-page"));
        }
        modelAndView.addObject("locations", locationManager.getAll());
        return modelAndView;
    }

    @GetMapping("/registration")
    public ModelAndView getRegistrationView() {
        return new ModelAndView("registration-page.html");
    }

    @GetMapping("/registration/fragment")
    public ModelAndView getRegistrationFragment() {
        return new ModelAndView("registration-page-fragment.html");
    }

    @GetMapping("/auth-page")
    public ModelAndView getAuthPage() {
        return new ModelAndView("authorization-page.html");
    }
    @GetMapping("/auth-page/fragment")
    public ModelAndView getAuthFragment() {
        return new ModelAndView("authorization-page-fragment.html");
    }

    @GetMapping("/main-page")
    public ModelAndView getMainPage() {
        ModelAndView modelAndView = new ModelAndView("main-page-authorized.html");
        try {
            List<LocationEntity> locations = locationManager.getAll();
            modelAndView.addObject("locations", locations);
            modelAndView.addObject("user", SecurityContextHolder.getContext().getAuthentication());
            modelAndView.addObject("locationData",
                    containerManager.getContainersByLocationName(locations.get(0).getNameOfLocation()));
        } catch (Exception e) {
            logger.error("[" + LocalDate.now() + "]" + "[ERROR] from " + Utils.getRequestRemoteAddr() + " with username = " + SecurityContextHolder.getContext().getAuthentication().getPrincipal() + " /main-page > [MainController] [ERROR]");
        }
        logger.info("[" + LocalDate.now() + "]" + "[INFO] from " + Utils.getRequestRemoteAddr() + " with username = " + SecurityContextHolder.getContext().getAuthentication().getPrincipal() + " /main-page > [MainController] [SUCCESS]");
        return modelAndView;
    }

    @PostMapping("/user/create")
    public ResponseEntity<String> userCreate(@RequestBody UserDto userDto) {
        try {
            User user = userManager.fromDto(userDto);
            userManager.save(user);
        } catch (Exception e) {
            logger.error("[" + LocalDate.now() + "]" + "[ERROR] from " + Utils.getRequestRemoteAddr() + " with username = " + SecurityContextHolder.getContext().getAuthentication().getPrincipal() + " /registration/user/create > [MainController] [ERROR]");
            throw new UserAlreadyExistException(e.getMessage());
        }
        logger.info("[" + LocalDate.now() + "]" + "[INFO] from " + Utils.getRequestRemoteAddr() + " with username = " + SecurityContextHolder.getContext().getAuthentication().getPrincipal() + " /user/create > [MainController] [SUCCESS]");
        return new ResponseEntity<>("Пользователь успешно создан!",
                HttpStatusCode.valueOf(200));
    }


    @ResponseBody
    @RequestMapping(value = "/image/{path}", method = RequestMethod.GET, produces = MediaType.IMAGE_JPEG_VALUE)
    @Cacheable("image")
    public byte[] image(@PathVariable String path) throws IOException {
        URL url = getClass().getResource("/static/image/" + path);
        assert url != null;
        InputStream in = url.openStream();
        return IOUtils.toByteArray(in);
    }
}
