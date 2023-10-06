package com.example.ctftreasuremapservice.manager;

import com.example.ctftreasuremapservice.entity.LocationEntity;
import com.example.ctftreasuremapservice.repository.LocationRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class LocationManager {

    private final LocationRepository locationRepository;

    public LocationManager(LocationRepository locationRepository) {
        this.locationRepository = locationRepository;
    }

    public List<LocationEntity> getAll() {
        return locationRepository.getAll();
    }

    public LocationEntity getByName(String name) {
        return locationRepository.getByName(name);
    }
}
