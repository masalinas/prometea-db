package com.thingtrack.prometea.config;

import java.util.Properties;

import javax.persistence.EntityManagerFactory;
import javax.sql.DataSource;

import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;
import org.springframework.jdbc.datasource.DriverManagerDataSource;
import org.springframework.orm.jpa.JpaTransactionManager;
import org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean;
import org.springframework.orm.jpa.vendor.HibernateJpaVendorAdapter;
import org.springframework.transaction.PlatformTransactionManager;
import org.springframework.transaction.annotation.EnableTransactionManagement;

@Configuration
@EnableTransactionManagement
@EnableJpaRepositories(basePackages = { "com.thingtrack.prometea.repository.prometea" },
					   entityManagerFactoryRef = "prometeaEntityManagerFactory",
					   transactionManagerRef = "prometeaTransactionManager")
public class PrometeaConfig {
	@Bean(name = "prometeaDataSource")
	public DataSource prometeaDataSource(){
      DriverManagerDataSource dataSource = new DriverManagerDataSource();
      
      dataSource.setDriverClassName("com.mysql.jdbc.Driver");
      dataSource.setUrl("jdbc:mysql://127.0.0.1:3306/trainingdb?autoReconnect=true&useUnicode=true&characterEncoding=UTF-8&allowMultiQueries=true&useSSL=false");
      dataSource.setUsername( "root" );
      dataSource.setPassword( "thingtrack" );
      
      return dataSource;
   	}
	   
    @Bean(name = "prometeaEntityManagerFactory")
    public LocalContainerEntityManagerFactoryBean prometeaEntityManagerFactory(@Qualifier("prometeaDataSource") DataSource dataSource) {
    	Properties properties = new Properties();
        properties.setProperty("hibernate.dialect", "org.hibernate.dialect.MySQLDialect");
                 
        LocalContainerEntityManagerFactoryBean em = new LocalContainerEntityManagerFactoryBean();
        
        em.setDataSource(dataSource);
        em.setPersistenceUnitName("prometeaPU");
        em.setPackagesToScan(new String[] { "com.thingtrack.prometea.domain.prometea" });
        em.setJpaVendorAdapter(new HibernateJpaVendorAdapter());
        em.setJpaProperties(properties);
        
        return em;
    }
    
    @Bean(name = "prometeaTransactionManager")
    public PlatformTransactionManager prometeaTransactionManager(@Qualifier("prometeaEntityManagerFactory") EntityManagerFactory entityManagerFactory) {
        return new JpaTransactionManager(entityManagerFactory);
    }
}
