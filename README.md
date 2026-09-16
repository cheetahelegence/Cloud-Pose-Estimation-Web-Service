# CloudPose — Cloud-Native Pose Estimation Web Service

CloudPose is a containerised pose estimation web service built with FastAPI and deployed on a Kubernetes cluster running on Oracle Cloud Infrastructure (OCI).

The project focuses on cloud deployment, containerisation, Kubernetes orchestration, load balancing, and performance testing rather than model development.

## Tech Stack

- Python
- FastAPI
- Docker
- Kubernetes
- Oracle Cloud Infrastructure (OCI)
- Locust
- REST API

## Architecture

Client
  ↓
FastAPI REST API
  ↓
Docker Container
  ↓
Kubernetes Service
  ↓
Kubernetes Pods
  ↓
Pose Estimation Model

## Key Features

- REST API for pose estimation requests
- Base64 image input and JSON responses
- Dockerised FastAPI application
- Kubernetes Deployment and Service configuration
- Multi-pod deployment and request distribution
- Load testing with Locust
- Performance testing under different pod counts and concurrent user loads

## Cloud & Kubernetes Setup

The application was deployed to a Kubernetes cluster running on OCI virtual machines.

The cluster consisted of:

- 1 controller node
- 2 worker nodes
- Kubernetes Deployment for managing application pods
- Kubernetes Service for exposing the API
- Resource limits configured for each pod
- Horizontal scaling across multiple pod replicas

## Load Testing

Locust was used to simulate concurrent users and evaluate the service under different Kubernetes pod configurations.

Experiments compared system behaviour with:

- 1 pod
- 2 pods
- 4 pods
- 8 pods

Metrics included response time, concurrent user capacity, and request success rate.

## Project Scope

This project was developed as part of Cloud Computing Course from Monash University.

The pose estimation model and inference helper code were provided as course materials. My work focused on:

- Building the FastAPI web service
- Containerising the application with Docker
- Deploying the service to Kubernetes on OCI
- Configuring Kubernetes Deployment and Service resources
- Scaling application pods
- Implementing Locust load testing
- Testing and analysing application performance

## Project Status

This project is no longer actively deployed. The repository is preserved as a portfolio and reference implementation.

Cloud infrastructure and original service endpoints are no longer active.
