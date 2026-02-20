//
//  AuthView.swift
//  NoteSpace
//
//  Created by User on 2026-02-19.
//

import SwiftUI

struct AuthView: View {
    @State private var isLoginMode = true
    @State private var email = ""
    @State private var username = ""
    @State private var password = ""
    @State private var showAlert = false
    @State private var alertMessage = ""
    
    @EnvironmentObject private var dataManager: DataManager
    
    var body: some View {
        NavigationView {
            VStack(spacing: 20) {
                Picker("Mode", selection: $isLoginMode) {
                    Text("Login").tag(true)
                    Text("Register").tag(false)
                }
                .pickerStyle(SegmentedPickerStyle())
                .padding()
                
                VStack(spacing: 15) {
                    TextField("Email", text: $email)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                        .autocapitalization(.none)
                        .keyboardType(.emailAddress)
                    
                    if !isLoginMode {
                        TextField("Username", text: $username)
                            .textFieldStyle(RoundedBorderTextFieldStyle())
                            .autocapitalization(.none)
                    }
                    
                    SecureField("Password", text: $password)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                }
                .padding(.horizontal)
                
                Button(action: handleAuth) {
                    Text(isLoginMode ? "Login" : "Register")
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(Color.blue)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                }
                .padding(.horizontal)
                
                Spacer()
            }
            .navigationTitle(isLoginMode ? "Welcome Back" : "Create Account")
            .alert(alertMessage, isPresented: $showAlert) {
                Button("OK", role: .cancel) { }
            }
        }
    }
    
    private func handleAuth() {
        if isLoginMode {
            if dataManager.login(email: email, password: password) {
                // Success
            } else {
                alertMessage = "Invalid credentials"
                showAlert = true
            }
        } else {
            if dataManager.register(email: email, username: username, password: password) {
                // Success
            } else {
                alertMessage = "Email already exists"
                showAlert = true
            }
        }
    }
}
