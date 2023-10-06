package org.example.servlets;

import jakarta.servlet.http.HttpServlet;
import org.example.dao.PirateDAO;
import org.example.services.TemplateProcessor;

abstract public class CtfHttpServlet extends HttpServlet {
    protected TemplateProcessor templateProcessor;
    protected PirateDAO pirateDAO;
    public CtfHttpServlet(TemplateProcessor templateProcessor, PirateDAO pirateDAO){
        this.templateProcessor = templateProcessor;
        this.pirateDAO = pirateDAO;
    }
}
