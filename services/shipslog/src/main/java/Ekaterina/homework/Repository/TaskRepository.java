package Ekaterina.homework.Repository;

import Ekaterina.homework.Entity.Task;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;


@Repository
public interface TaskRepository extends JpaRepository<Task, Integer> {
    List<Task> findTaskByAccessId(String accessId);
    boolean deleteTaskByAccessId(String accessId);
}