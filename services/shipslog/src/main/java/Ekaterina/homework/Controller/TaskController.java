package Ekaterina.homework.Controller;

import Ekaterina.homework.Entity.Task;
import Ekaterina.homework.Service.TaskService;
import org.antlr.v4.runtime.misc.Utils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.security.NoSuchAlgorithmException;
import java.time.LocalDate;
import java.util.List;


@Controller
public class TaskController {

    private final Logger logger = LoggerFactory.getLogger("TaskController");

    public String verificationCodeStr = "0";
    @Autowired
    private TaskService taskService;

    @GetMapping("/private-news")
    public String getPrivateNews(Model model) {
        List<Task> taskList = taskService.getAll();
        model.addAttribute("taskList", taskList);
        model.addAttribute("taskSize", taskList.size());
        return "shipping_log";
    }


    @PostMapping("/add")
    public String addTask(@ModelAttribute Task task) throws NoSuchAlgorithmException {
        taskService.save(task);
        verificationCodeStr = task.getAccessId();
        logger.info("["+ LocalDate.now() + "]" + "[INFO] Task ID: " + task.getId().toString() + " with access ID: " + task.getAccessId() + " /add > [AddTask Controller] [SUCCESS]");
        return "redirect:/verification-code";
    }

    @GetMapping("/verification-code")
    public String getVerificationCode(Model model){
        model.addAttribute("verificationCode", verificationCodeStr);
        verificationCodeStr = "0";
        return "verificationCode";
    }

    @GetMapping("/check")
    public String check(Model model){
        model.addAttribute("taskSize", 0);
        model.addAttribute("taskList", null);
        return "checkCode";
    }

    @PostMapping("/checkCode")
    public String checkCode(@RequestParam (required = true, defaultValue = "" ) String verificationCode, Model model){
        if (verificationCode!=null)
        {
            List<Task> taskList = taskService.getByCode(verificationCode);
            if (taskList.size()==0){
                logger.error("["+ LocalDate.now() + "]" + "[ERROR] Try to get access with incorrect verification code "
                        + verificationCode
                        + " /checkCode > [CheckCode Controller] [ERROR]");
            }
            else{
                logger.info("[" + LocalDate.now() + "]" + "[INFO] Task with verification code: "
                        + verificationCode + " accessed "
                        + " /checkCode > [CheckCode Controller] [SUCCESS]");
            }
                model.addAttribute("taskList", taskList);
                model.addAttribute("taskSize", taskList.size());
        }
        else{
            model.addAttribute("taskSize", 0);
            model.addAttribute("taskList", null);
            logger.error("["+ LocalDate.now() + "]" + "[ERROR] Try to get access with no verification code "
                    + " /checkCode > [CheckCode Controller] [ERROR]");
        }
        return "checkCode";
    }


    @GetMapping("/news")
    public String getAll(Model model) {
        List<Task> taskList = taskService.getAll();
        model.addAttribute("taskList", taskList);
        model.addAttribute("taskSize", taskList.size());
        return "news";
    }


}