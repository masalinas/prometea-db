package com.thingtrack.prometea.repository.prometea;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.thingtrack.prometea.domain.prometea.Patient;

@Repository
public interface PatientRepository extends JpaRepository<Patient, Long> {    
}