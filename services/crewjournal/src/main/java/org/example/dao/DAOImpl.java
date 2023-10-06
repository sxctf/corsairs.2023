package org.example.dao;

import org.example.model.Pirate;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.Transaction;

import java.util.List;
import java.util.Optional;

public abstract class DAOImpl<T> implements DAO<T>{

    final protected SessionFactory sessionFactory;
    protected Class<T> entityClass;

    public DAOImpl(SessionFactory sessionFactory, Class<T> entityClass){
        this.sessionFactory = sessionFactory;
        this.entityClass = entityClass;
    }
    @Override
    public Optional<T> findByID(long id) {
        return Optional.empty();
    }

    @Override
    public long save(T t) {
        Session session = sessionFactory.openSession();
        Transaction tx = session.beginTransaction();
        session.persist(t);
        tx.commit();
        session.close();
        return 0;
    }

    @Override
    public List<T> findAll() {
        Session session = sessionFactory.openSession();
        Transaction tx = session.beginTransaction();
        List<T> pirateList = session.createQuery("select p from " + entityClass.getName() + " p", entityClass).getResultList();
        tx.commit();
        session.close();
        return pirateList;
    }

    @Override
    public void update(T t) {
        org.hibernate.Transaction tx = null;
        try (Session session = sessionFactory.openSession()){
            tx = session.beginTransaction();
            session.update(t);
            tx.commit();
        } catch (Exception e) {
            if(tx!=null) tx.rollback();
        }
    }
}
