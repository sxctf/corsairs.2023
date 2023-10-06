package org.example.servlets.api;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.example.dao.PirateDAO;
import org.example.server.CrewJournalServer;
import org.example.services.TemplateProcessor;
import org.example.servlets.CtfHttpServlet;
import java.io.IOException;
import java.util.stream.Collectors;

public class PirateServlet extends CtfHttpServlet {

    final private Gson gson = new GsonBuilder().serializeNulls().setPrettyPrinting().excludeFieldsWithoutExposeAnnotation().create();

    public PirateServlet(TemplateProcessor templateProcessor, PirateDAO pirateDAO) {
        super(templateProcessor, pirateDAO);
    }

    @Override
    public void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
        CrewJournalServer.logger.info("from {} req: {} GET Request", request.getRemoteAddr(), request.getRequestURI());
        response.setContentType("application/json;charset=UTF-8");
        var pirateList = pirateDAO.findAll().stream().filter(pirate -> !pirate.getRank().equals("young")).collect(Collectors.toList());
        response.getOutputStream().print(gson.toJson(pirateList));
    }
}
