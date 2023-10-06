package org.example.servlets;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import org.example.dao.PirateDAO;
import org.example.model.Pirate;
import org.example.services.TemplateProcessor;

import java.io.IOException;

public class ConfirmServlet extends CtfHttpServlet {
    public ConfirmServlet(TemplateProcessor templateProcessor, PirateDAO pirateDAO){
        super(templateProcessor, pirateDAO);
    }
    @Override
    public void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
        HttpSession httpSession = request.getSession(false);
        if (httpSession != null) {
            Pirate pirate = pirateDAO.findByhashNewAndCurrentPassword(request.getParameter("hash")).get();
            pirate.setPassword(pirate.getNewPassword());
            pirate.setNewPassword(null);
            pirate.setHashNewAndCurrentPassword(null);
            pirateDAO.update(pirate);
            response.sendRedirect("/welcome");
        }
    }
}
