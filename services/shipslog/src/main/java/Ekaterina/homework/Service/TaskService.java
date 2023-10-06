package Ekaterina.homework.Service;

import Ekaterina.homework.Entity.Task;
import Ekaterina.homework.Repository.TaskRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;

import java.math.BigInteger;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.List;
import java.util.UUID;

@Service
public class TaskService {

    @Autowired
    private TaskRepository taskRepository;

    public List<Task> getAll() {
        return taskRepository.findAll(Sort.by(Sort.Order.asc("date"),
                Sort.Order.desc("id")));
    }

    public List<Task> getByCode(String verificationCode){
        return taskRepository.findTaskByAccessId(verificationCode);
    }

    public Task save(Task task) throws NoSuchAlgorithmException {

        UUID uuid = UUID.randomUUID();
        task.setId(uuid);

        String plainText = task.getName() + task.getDestination() + task.getStatus()+ task.getId().toString();
        MessageDigest messageDigest = MessageDigest.getInstance("MD5");
        messageDigest.reset();
        messageDigest.update(plainText.getBytes(StandardCharsets.UTF_8));
        byte[] digest = messageDigest.digest();
        BigInteger bigInteger = new BigInteger(1, digest);
        task.setAccessId( bigInteger.toString(16));

        return taskRepository.save(task);
    }

}