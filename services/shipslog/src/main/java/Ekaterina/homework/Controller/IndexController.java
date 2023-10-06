package Ekaterina.homework.Controller;

import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

public class IndexController {
    @GetMapping("/")
    public String registration(Model model) {

        return "index";
    }
}
