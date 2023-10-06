package org.example.model;

import com.google.gson.annotations.Expose;
import com.opencsv.bean.CsvBindByPosition;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import org.example.services.HashGenerator;

@Entity
@Table(name = "Crew")
public class Pirate {
    @Id
    @GeneratedValue()
    private long id;

    @CsvBindByPosition(position = 0)
    private String name;
    @CsvBindByPosition(position = 1)
    private String rank;
    @Expose
    @CsvBindByPosition(position = 2)
    private String login;
    @Expose
    @CsvBindByPosition(position = 3)
    private String password;
    @CsvBindByPosition(position = 4)
    private String passport;    //The flag
    private String sessionID;
    @CsvBindByPosition(position = 5)
    private String email;
    private String newPassword;
    private String hashNewAndCurrentPassword;
    private String marque;  //The flag hash

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public Pirate() {
    }

    public String getName() {
        return this.name;
    }

    public long getId(){
        return this.id;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getRank() {
        return rank;
    }

    public void setRank(String rank) {
        this.rank = rank;
    }

    public String getPassport() {
        return passport;
    }

    public String getPassword() {
        return password;
    }

    public void setPassport(String passport) {
        this.passport = passport;
        this.marque = HashGenerator.hashFrom(this.passport);
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public String getLogin(){
        return this.login;
    }

    public void setLogin(String login){
        this.login = login;
    }

    public String getSessionID() {
        return sessionID;
    }

    public void setSessionID(String sessionID){
        this.sessionID = sessionID;
    }

    @Override
    public String toString(){
        return "" + id + " " + this.name + " " + this.rank + " " + this.login + " " + this.password + " " + this.email;
    }

    public String getNewPassword() {
        return newPassword;
    }

    public void setNewPassword(String newPassword) {
        this.newPassword = newPassword;
    }

    public String getHashNewAndCurrentPassword() {
        return hashNewAndCurrentPassword;
    }

    public void setHashNewAndCurrentPassword(String hashNewAndCurrentPassword) {
        this.hashNewAndCurrentPassword = hashNewAndCurrentPassword;
    }
}
