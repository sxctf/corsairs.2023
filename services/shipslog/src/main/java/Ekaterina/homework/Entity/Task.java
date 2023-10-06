package Ekaterina.homework.Entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import org.springframework.format.annotation.DateTimeFormat;

import java.security.NoSuchAlgorithmException;
import java.util.Date;
import java.util.UUID;

@Entity
@Table(name="TASK")
public class Task {

    @Column (name = "id")
    @Id
    private UUID id;

    @Column (name = "name")
    private String name;

    @Column (name = "destination")
    private String destination;

    @Column (name = "description")
    private String description;

    @Column (name = "date")
    private Date date;

    @Column (name = "status")
    private String status;

    @Column(name = "ACCESSID")
    private String accessId;

    public Task() {
    }

    public Task(UUID id, String name, String destination, String description, Date date, String status, String accessId) throws NoSuchAlgorithmException {
        this.id = id;
        this.destination = destination;
        this.name = name;
        this.description = description;
        this.date = date;
        this.status = status;
        this.accessId = accessId;
    }

    public String getAccessId() {
        return accessId;
    }

    public void setAccessId(String accessId) {
        this.accessId = accessId;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getDestination() {
        return destination;
    }

    public void setDestination(String destination) {
        this.destination = destination;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public Date getDate() {
        return date;
    }

    @DateTimeFormat(pattern = "yyyy-MM-dd")
    public void setDate(Date date) {
        this.date = date;
    }
}