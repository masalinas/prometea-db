package com.thingtrack.prometea.repository.cardio;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.thingtrack.prometea.domain.cardio.Patient;

@Repository
public interface PatientRepository extends JpaRepository<Patient, Long> {    
}