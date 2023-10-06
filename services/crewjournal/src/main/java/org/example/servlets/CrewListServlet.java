package org.example.servlets;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import org.example.dao.PirateDAO;
import org.example.model.Pirate;
import org.example.services.MailConfirmation;
import org.example.services.TemplateProcessor;
import org.example.services.HashGenerator;
import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class CrewListServlet extends CtfHttpServlet {

    MailConfirmation mailConfirmation;
    public CrewListServlet(TemplateProcessor templateProcessor, PirateDAO pirateDAO, MailConfirmation mailConfirmation) {
        super(templateProcessor, pirateDAO);
        this.mailConfirmation = mailConfirmation;
    }

    @Override
    public void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
        HttpSession httpSession = request.getSession(false);
        if (httpSession != null) {
            List<Pirate> pirateList = pirateDAO.findAll();
            Boolean isUserCaptain = false;
            for(Pirate pirate : pirateList){
                if(pirate.getSessionID() == null || !pirate.getSessionID().equals(httpSession.getId())){
                    pirate.setSessionID("");
                }
                if(pirate.getSessionID().equals(httpSession.getId()) && pirate.getRank().equals("captain")){
                    isUserCaptain = true;
                }
            }
            Map<String, Object> hash = new HashMap<>();
            hash.put("pirateList", pirateList);
            hash.put("isUserCaptain", isUserCaptain);
            response.getWriter().print(templateProcessor.getPage("crewList.html", hash));
        } else {
            response.sendRedirect("/login");
        }
    }

    @Override
    public void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException {
        if (request.getSession(false) != null) {
            var map = request.getParameterMap();
            List<Pirate> pirateList = pirateDAO.findAll();
            for (Pirate pirate : pirateList) {
                if (Long.parseLong(map.get("id_field")[0]) == pirate.getId()) {
                    if(map.containsKey("password_field1")) {
                        pirate.setNewPassword(map.get("password_field1")[0]);
                        String passwordsHash = HashGenerator.hashFrom(pirate.getPassword() + pirate.getNewPassword());
                        pirate.setHashNewAndCurrentPassword(passwordsHash);
                        String bodyText = "<p>Dear " + pirate.getName() + ", to complete your password changing, please go to this link: <a " + "href=\"http://"
                        + request.getHeader("Host") + "/confirm?hash=" + passwordsHash + "\">Confirm</a></p>";
                        mailConfirmation.sendEmail(pirate.getEmail(), "ctf-crew@mail.ru", "TU0y235LtjRDbrJ9mN06", "Confirm password changing", bodyText);
                    }
                    if(map.containsKey("email_field")) {
                        pirate.setEmail(map.get("email_field")[0]);
                    }
                    if(map.containsKey("rank_field")) {
                        pirate.setRank(map.get("rank_field")[0]);
                    }
                    pirateDAO.update(pirate);
                    break;
                }
            }
            response.sendRedirect("/crewList");
        } else {
            response.sendRedirect("/login");
        }
    }
}
