package org.example;

import com.opencsv.bean.CsvToBeanBuilder;
import org.example.dao.PirateDAO;
import org.example.dao.PirateDAOImpl;
import org.example.model.Pirate;
import org.example.services.*;
import org.hibernate.SessionFactory;
import org.hibernate.boot.MetadataSources;
import org.hibernate.boot.registry.StandardServiceRegistryBuilder;
import org.example.server.*;
import java.io.FileReader;
import java.util.List;

public class CrewJournal {
    private static final int WEB_SERVER_PORT = 9000;
    private static final String TEMPLATES_DIR = "src/main/resources/web";
    public static final String HIBERNATE_CFG_FILE = "hibernate.cfg.xml";



    public static void main(String[] args) throws Exception {

        String csvFileName = null;
        SessionFactory sessionFactory = new MetadataSources(new StandardServiceRegistryBuilder().configure(HIBERNATE_CFG_FILE).build())
                .addAnnotatedClass(Pirate.class).buildMetadata().buildSessionFactory();
        PirateDAO pirateDAO = new PirateDAOImpl(sessionFactory);
        for (int i=0; i<args.length; i++){
            if (args[i].equals("-csvInput") && i < args.length - 1) {
                csvFileName = args[i + 1];
            }
            if (args[i].equals("-ip") && i < args.length - 1) {
            }
        }
        if(csvFileName!=null){
            dbInit(csvFileName, pirateDAO);
        }
        TemplateProcessor templateProcessor = new TemplateProcessorImpl(TEMPLATES_DIR);
        AuthService authService = new AuthServiceImpl(pirateDAO);
        MailConfirmation mailConfirmation  = new MailConfirmation();
        CrewJournalServer crewJournalServer = new CrewJournalServer(WEB_SERVER_PORT, pirateDAO, templateProcessor, authService, mailConfirmation);
        crewJournalServer.start();
        crewJournalServer.join();
    }

    public static int getWebServerPort(){
        return WEB_SERVER_PORT;
    }

    private static void dbInit(String csvFileName, PirateDAO pirateDAO){
        try(FileReader fileReader = new FileReader(csvFileName)) {
            List<Pirate> pirateList = new CsvToBeanBuilder<Pirate>(fileReader)
                    .withType(Pirate.class)
                    .withSeparator(';')
                    .build().parse();
            pirateList.stream().filter(pirate -> pirateDAO.findByLogin(pirate.getLogin()).isEmpty()).forEach(pirateDAO::save);
        } catch (Exception e){
            e.printStackTrace();
        }
    }
}
