package com.thingtrack.prometea.controller.cardio;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;

import com.thingtrack.prometea.domain.cardio.Patient;
import com.thingtrack.prometea.repository.cardio.PatientRepository;

public class PatientController {
    @Autowired
    private PatientRepository patientRepository;
    
    public List<Patient> getAllPatients() {
        List<Patient> patiens = patientRepository.findAll();

        return patiens;
    }
}
