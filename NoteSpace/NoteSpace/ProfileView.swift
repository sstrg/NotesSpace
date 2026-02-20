//
//  ProfileView.swift
//  NoteSpace
//
//  Created by User on 2026-02-19.
//

import SwiftUI

struct ProfileView: View {
    @EnvironmentObject private var dataManager: DataManager
    @State private var showingClearAlert = false
    
    var body: some View {
        NavigationView {
            List {
                if let user = dataManager.currentUser {
                    Section("User Info") {
                        HStack {
                            Text("Username")
                            Spacer()
                            Text(user.username)
                                .foregroundColor(.gray)
                        }
                        
                        HStack {
                            Text("Email")
                            Spacer()
                            Text(user.email)
                                .foregroundColor(.gray)
                        }
                        
                        HStack {
                            Text("Spaces")
                            Spacer()
                            Text("\(user.spaceIds.count)")
                                .foregroundColor(.gray)
                        }
                    }
                    
                    Section("My Spaces (as Creator)") {
                        let createdSpaces = dataManager.spaces.filter { $0.creatorId == user.id }
                        if createdSpaces.isEmpty {
                            Text("No spaces created")
                                .foregroundColor(.gray)
                                .italic()
                        } else {
                            ForEach(createdSpaces) { space in
                                VStack(alignment: .leading) {
                                    Text(space.name)
                                        .font(.headline)
                                    Text(space.description)
                                        .font(.caption)
                                        .foregroundColor(.gray)
                                    Text("\(space.memberIds.count) members")
                                        .font(.caption)
                                        .foregroundColor(.blue)
                                }
                            }
                        }
                    }
                    
                    Section("Spaces I Admin") {
                        let adminSpaces = dataManager.spaces.filter { space in
                            space.adminIds.contains(user.id) && space.creatorId != user.id
                        }
                        if adminSpaces.isEmpty {
                            Text("No admin spaces")
                                .foregroundColor(.gray)
                                .italic()
                        } else {
                            ForEach(adminSpaces) { space in
                                VStack(alignment: .leading) {
                                    Text(space.name)
                                        .font(.headline)
                                    Text(space.description)
                                        .font(.caption)
                                        .foregroundColor(.gray)
                                    HStack {
                                        Image(systemName: "shield.fill")
                                            .font(.caption)
                                            .foregroundColor(.blue)
                                        Text("Admin")
                                            .font(.caption)
                                            .foregroundColor(.blue)
                                    }
                                }
                            }
                        }
                    }
                    
                    Section("Other Spaces") {
                        let otherSpaces = dataManager.spaces.filter { space in
                            space.memberIds.contains(user.id) &&
                            space.creatorId != user.id &&
                            !space.adminIds.contains(user.id)
                        }
                        if otherSpaces.isEmpty {
                            Text("No other spaces")
                                .foregroundColor(.gray)
                                .italic()
                        } else {
                            ForEach(otherSpaces) { space in
                                VStack(alignment: .leading) {
                                    Text(space.name)
                                        .font(.headline)
                                    Text(space.description)
                                        .font(.caption)
                                        .foregroundColor(.gray)
                                    Text("Member")
                                        .font(.caption)
                                        .foregroundColor(.green)
                                }
                            }
                        }
                    }
                }
                
                Section {
                    Button(action: logout) {
                        Text("Logout")
                            .foregroundColor(.red)
                    }
                }
                
              
                Section(header: Text("Debug")) {
                    Button(action: { showingClearAlert = true }) {
                        HStack {
                            Image(systemName: "trash")
                                .foregroundColor(.orange)
                            Text("Clear All Data")
                                .foregroundColor(.orange)
                        }
                    }
                }
            }
            .navigationTitle("Profile")
            .alert("Clear All Data", isPresented: $showingClearAlert) {
                Button("Cancel", role: .cancel) { }
                Button("Clear", role: .destructive) {
                    clearAllData()
                }
            } message: {
                Text("This will delete all users, spaces, and notes. This action cannot be undone.")
            }
        }
    }
    
    private func logout() {
        dataManager.logout()
    }
    
    private func clearAllData() {
       
        UserDefaults.standard.removeObject(forKey: "users")
        UserDefaults.standard.removeObject(forKey: "spaces")
        UserDefaults.standard.removeObject(forKey: "notes")
        UserDefaults.standard.removeObject(forKey: "currentUser")
        
      
        dataManager.logout()
        
        print("🧹 All data cleared")
    }
}
