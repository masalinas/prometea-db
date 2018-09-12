package com.thingtrack.prometea.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;

import com.thingtrack.prometea.domain.Patient;
import com.thingtrack.prometea.repository.PatientRepository;

public class PatientController {
    @Autowired
    private PatientRepository patientRepository;
    
    public List<Patient> getAllPatients() {
        List<Patient> patiens = patientRepository.findAll();

        return patiens;
    }
}
