package org.example.dao;

import jakarta.persistence.NoResultException;
import org.example.model.Pirate;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.Transaction;
import java.util.Optional;

public class PirateDAOImpl extends DAOImpl<Pirate> implements PirateDAO
{
    public PirateDAOImpl(SessionFactory sessionFactory) {
        super(sessionFactory, Pirate.class);
    }

    @Override
    public Optional<Pirate> findByLogin(String login) {
        try(Session session = sessionFactory.openSession()){
            Transaction tx = session.beginTransaction();
            var query = session.createQuery("select p from " + entityClass.getName() + " p where p.login = :login", entityClass).setParameter("login", login);
            Pirate pirate = query.getSingleResult();
            tx.commit();
            return Optional.of(pirate);
        } catch (NoResultException e) {
            return Optional.empty();
        }
    }
    @Override
    public Optional<Pirate> findByhashNewAndCurrentPassword(String hashNewAndCurrentPassword){
        Session session = sessionFactory.openSession();
        Transaction tx = session.beginTransaction();
        var query = session.createQuery("select p from " + entityClass.getName() + " p where p.hashNewAndCurrentPassword = :hashNewAndCurrentPassword", entityClass).setParameter("hashNewAndCurrentPassword", hashNewAndCurrentPassword);
        Pirate pirate = query.getSingleResult();
        tx.commit();
        session.close();
        return Optional.of(pirate);
    }

    @Override
    public String findPassportByMarque(String marque) {
        Session session = sessionFactory.openSession();
        Transaction tx = session.beginTransaction();
        var query = session.createQuery("select p.passport from " + entityClass.getName() + " p where p.marque = :marque", String.class).setParameter("marque", marque);
        String flag = query.getSingleResult();
        tx.commit();
        session.close();
        return flag;
    }
}
