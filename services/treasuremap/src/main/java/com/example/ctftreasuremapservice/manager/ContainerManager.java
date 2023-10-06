package com.example.ctftreasuremapservice.manager;

import com.example.ctftreasuremapservice.entity.ContainerEntity;
import com.example.ctftreasuremapservice.repository.ContainerRepository;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ContainerManager {

    private final ContainerRepository containerRepository;
    private final LocationManager locationManager;
    private final UserManager userManager;

    public ContainerManager(ContainerRepository containerRepository, LocationManager locationManager, UserManager userManager) {
        this.containerRepository = containerRepository;
        this.locationManager = locationManager;
        this.userManager = userManager;
    }

    public void saveContainer(String treasure, String nameOfLocation) {
        String author = SecurityContextHolder.getContext().getAuthentication().getPrincipal().toString();
        ContainerEntity newContainer = new ContainerEntity(
                treasure,
                author,
                locationManager.getByName(nameOfLocation));
        containerRepository.save(newContainer);

    }

    public List<ContainerEntity> getContainersByLocationName(String locationName) {
        if (userManager.isAdmin()) {
            return containerRepository.getAllByLocationName(locationName);
        } else {
            return containerRepository.getContainerByLocationNameAndAuthor(locationName,
                    SecurityContextHolder.getContext().getAuthentication().getPrincipal().toString());
        }
    }

}
