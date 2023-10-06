package com.example.ctftreasuremapservice.utils;

import com.example.ctftreasuremapservice.exception.BadCredentialsFormatException;
import com.example.ctftreasuremapservice.model.pojo.User;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;

public class Utils {
    public static String getRequestRemoteAddr() {
        HttpServletRequest request = ((ServletRequestAttributes) RequestContextHolder
                .currentRequestAttributes()).getRequest();
        return request.getRemoteAddr();
    }

    public static void checkCredentials(User user) {
        if (user.getUsername().equals("")) {
            throw new BadCredentialsFormatException("Имя пользователя не может быть пустым!");
        } else if (user.getPassword().equals("")) {
            throw new BadCredentialsFormatException("Пароль не может быть пустым!");
        } else if (user.getUsername().length() < 5) {
            throw new BadCredentialsFormatException("Имя пользователя должно состоять минимум из 5 символов!");
        } else if (user.getPassword().length() < 5) {
            throw new BadCredentialsFormatException("Пароль должен состоять минимум из 5 символов!");
        }
    }
}
