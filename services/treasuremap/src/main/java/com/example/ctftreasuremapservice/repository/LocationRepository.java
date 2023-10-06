package com.example.ctftreasuremapservice.repository;


import com.example.ctftreasuremapservice.entity.LocationEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public
interface LocationRepository extends JpaRepository<LocationEntity, String> {
    @Query("select location from LocationEntity location")
    List<LocationEntity> getAll();

    @Query("select location from LocationEntity location where location.nameOfLocation=:name")
    LocationEntity getByName(String name);
}
