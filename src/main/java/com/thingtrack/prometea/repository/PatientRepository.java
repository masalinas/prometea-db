package com.thingtrack.prometea.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.thingtrack.prometea.domain.Patient;

@Repository
public interface PatientRepository extends JpaRepository<Patient, Long> {    
}