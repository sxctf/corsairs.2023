package org.example.dao;

import java.util.List;
import java.util.Optional;

public interface DAO<T> {
    Optional<T> findByID(long id);
    long save(T t);
    List<T> findAll();
    void update(T t);
}
