//
//  CreateSpaceView.swift
//  NoteSpace
//
//  Created by User on 2026-02-19.
//

import SwiftUI

struct CreateSpaceView: View {
    @Environment(\.dismiss) var dismiss
    @EnvironmentObject private var dataManager: DataManager
    
    @State private var name = ""
    @State private var description = ""
    
    var body: some View {
        NavigationView {
            Form {
                TextField("Space Name", text: $name)
                TextField("Description", text: $description)
            }
            .navigationTitle("Create Space")
            .navigationBarItems(
                leading: Button("Cancel") { dismiss() },
                trailing: Button("Create") {
                    if let userId = dataManager.currentUser?.id {
                        let newSpace = dataManager.createSpace(
                            name: name,
                            description: description,
                            creatorId: userId
                        )
                        
                        var updatedUser = dataManager.currentUser
                        updatedUser?.spaceIds.append(newSpace.id)
                        if let user = updatedUser {
                            dataManager.currentUser = user
                        }
                        
                        dataManager.loadUserSpaces()
                        dismiss()
                    }
                }
                .disabled(name.isEmpty)
            )
        }
    }
}
