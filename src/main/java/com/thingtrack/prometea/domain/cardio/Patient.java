package com.thingtrack.prometea.domain.cardio;

import java.io.Serializable;
import java.util.Date;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;
import javax.persistence.Temporal;
import javax.persistence.TemporalType;

@Entity
@Table(name = "Paciente")
public class Patient implements Serializable  {
	private static final long serialVersionUID = 1724817692113228260L;
	
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
	private long id;
	
    @Column(nullable = false, name = "centro", columnDefinition="VARCHAR(10)")
	private String center;
	
    @Column(nullable = false, columnDefinition="VARCHAR(10)")
	private String nhc;
	
    @Column(nullable = false, columnDefinition="CHAR(1)")
	private String sex;
	
    @Column(columnDefinition="VARCHAR(20)")
	private String cias;
	
    @Column(columnDefinition="CHAR(1)")
	private String location;
	
    @Column(columnDefinition="CHAR(1)")
	private String typePac;
	
	@Temporal(TemporalType.DATE)
	private Date birthDate;
	
	@Temporal(TemporalType.DATE)
	private Date exitus;
	
	@Column(columnDefinition="VARCHAR(20)")
	private String identification;
	
	public long getId() {
		return id;
	}

	public String getCenter() {
		return center;
	}

	public void setCenter(String center) {
		this.center = center;
	}

	public String getNhc() {
		return nhc;
	}

	public void setNhc(String nhc) {
		this.nhc = nhc;
	}

	public String getSex() {
		return sex;
	}

	public void setSex(String sex) {
		this.sex = sex;
	}

	public String getCias() {
		return cias;
	}

	public void setCias(String cias) {
		this.cias = cias;
	}

	public String getLocation() {
		return location;
	}

	public void setLocation(String location) {
		this.location = location;
	}

	public String getTypePac() {
		return typePac;
	}

	public void setTypePac(String typePac) {
		this.typePac = typePac;
	}

	public Date getBirthDate() {
		return birthDate;
	}

	public void setBirthDate(Date birthDate) {
		this.birthDate = birthDate;
	}

	public Date getExitus() {
		return exitus;
	}

	public void setExitus(Date exitus) {
		this.exitus = exitus;
	}

	public String getIdentification() {
		return identification;
	}

	public void setIdentification(String identification) {
		this.identification = identification;
	} 
	
	@Override
	public int hashCode() {
		final int prime = 31;
		int result = 1;
		result = prime * result + (int) (id ^ (id >>> 32));
		return result;
	}

	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (getClass() != obj.getClass())
			return false;
		Patient other = (Patient) obj;
		if (id != other.id)
			return false;
		return true;
	}
	@Override
	public String toString() {
		return "Patient [id=" + id + "]";
	}

}
