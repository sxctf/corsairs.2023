package org.example.dao;

import org.example.model.Pirate;
import java.util.Optional;

public interface PirateDAO extends DAO<Pirate>{
        Optional<Pirate> findByLogin(String login);
        Optional<Pirate> findByhashNewAndCurrentPassword(String hashNewAndCurrentPassword);
        String findPassportByMarque(String marque);
}
