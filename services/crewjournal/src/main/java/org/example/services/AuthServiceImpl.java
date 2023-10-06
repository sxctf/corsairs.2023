package org.example.services;

import org.example.dao.PirateDAO;

public class AuthServiceImpl implements AuthService {

    final private PirateDAO pirateDAO;
    public AuthServiceImpl(PirateDAO pirateDAO){
        this.pirateDAO = pirateDAO;
    }
    @Override
    public boolean authenticate(String login, String password) {
        var pirateOptional = pirateDAO.findByLogin(login);
        return pirateOptional.isEmpty()?false:pirateOptional.get().getPassword().equals(password);
    }
}
