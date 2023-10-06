package org.example.servlets;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.example.dao.PirateDAO;
import org.example.model.Pirate;
import org.example.server.CrewJournalServer;
import org.example.services.HashGenerator;
import org.example.services.TemplateProcessor;

import java.io.IOException;

public class AddPirate extends CtfHttpServlet{

    public AddPirate(TemplateProcessor templateProcessor, PirateDAO pirateDAO) {
        super(templateProcessor, pirateDAO);
    }

    @Override
    public void doPost(HttpServletRequest request, HttpServletResponse response){
        var map = request.getParameterMap();
        Pirate pirate = new Pirate();
        pirate.setName(map.get("name_field")[0]);
        pirate.setRank(map.get("rank_field")[0]);
        pirate.setLogin(map.get("login_field")[0]);
        pirate.setPassword(map.get("password_field")[0]);
        pirate.setPassport(map.get("passport_field")[0]);
        pirate.setEmail(map.get("email_field")[0]);
        pirateDAO.save(pirate);
        try {
            response.getOutputStream().print(HashGenerator.hashFrom(pirate.getPassport()));
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        CrewJournalServer.logger.info("from {} req: {} POST Request. Pirate ({}) is added", request.getRemoteAddr(), request.getRequestURL(), pirate);
    }
}
