package org.example.server;

import org.eclipse.jetty.server.Server;
import org.eclipse.jetty.server.handler.ResourceHandler;
import org.eclipse.jetty.servlet.DefaultServlet;
import org.eclipse.jetty.servlet.ServletContextHandler;
import org.eclipse.jetty.servlet.ServletHolder;
import org.example.dao.PirateDAO;
import org.example.services.AuthService;
import org.example.services.MailConfirmation;
import org.example.services.TemplateProcessor;
import org.example.servlets.*;
import org.example.servlets.api.PirateServlet;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class CrewJournalServer {

    public static final Logger logger = LoggerFactory.getLogger(CrewJournalServer.class);

    private final Server server;
    private final PirateDAO pirateDAO;
    private final TemplateProcessor templateProcessor;
    private final AuthService authService;
    private final MailConfirmation mailConfirmation;

    public CrewJournalServer(int webServerPort, PirateDAO pirateDAO, TemplateProcessor templateProcessor, AuthService authService, MailConfirmation mailConfirmation) {
        this.pirateDAO = pirateDAO;
        this.server = new Server(webServerPort);
        this.templateProcessor = templateProcessor;
        this.authService = authService;
        this.mailConfirmation = mailConfirmation;
    }

    public void start() throws Exception {
        if (server.getHandlers().length == 0) {
            initContext();
        }
        server.start();
    }

    public void join() {
        try {
            server.join();
        } catch (Exception e){
            e.printStackTrace();
        }
    }

    private void initContext(){
        ServletContextHandler servletContextHandler = new ServletContextHandler(ServletContextHandler.SESSIONS);
        servletContextHandler.setContextPath("/");
        ServletHolder welcomePageServletHolder = new ServletHolder(new WelcomePageServlet(templateProcessor,pirateDAO));
        servletContextHandler.addServlet(welcomePageServletHolder, "/welcome");
        ServletHolder confirmServletHolder = new ServletHolder(new ConfirmServlet(templateProcessor,pirateDAO));
        servletContextHandler.addServlet(confirmServletHolder, "/confirm");
        ServletHolder crewListServletHolder = new ServletHolder(new CrewListServlet(templateProcessor, pirateDAO, mailConfirmation));
        servletContextHandler.addServlet(crewListServletHolder, "/crewList");
        ServletHolder addPirateServletHolder = new ServletHolder(new AddPirate(templateProcessor, pirateDAO));
        servletContextHandler.addServlet(addPirateServletHolder, "/addPirate");
        ServletHolder loginServletHolder = new ServletHolder(new LoginServlet(templateProcessor, pirateDAO, authService));
        servletContextHandler.addServlet(loginServletHolder, "/login");
        ServletHolder defaultServletHolder = servletContextHandler.addServlet(DefaultServlet.class, "/");
        ServletHolder pirateServletHolder = new ServletHolder(new PirateServlet(templateProcessor,pirateDAO));
        servletContextHandler.addServlet(pirateServletHolder, "/api/pirates");
        ServletHolder flagFromFlagHashServletHolder = new ServletHolder(new PassportFromMarqueServlet(templateProcessor,pirateDAO));
        servletContextHandler.addServlet(flagFromFlagHashServletHolder, "/getPassportFromMarque");
        defaultServletHolder.setInitParameter("resourceBase", "src/main/resources/web/static");
        defaultServletHolder.setInitParameter("dirAllowed", "false");
        servletContextHandler.setWelcomeFiles(new String[]{"login.html"});
        server.setHandler(servletContextHandler);
    }

    private ResourceHandler createResourceHandler() {
        ResourceHandler resourceHandler = new ResourceHandler();
        resourceHandler.setDirectoriesListed(false);
        resourceHandler.setResourceBase("src/main/resources/web");
        return resourceHandler;
    }
}
