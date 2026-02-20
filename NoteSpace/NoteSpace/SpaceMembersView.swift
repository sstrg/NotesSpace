//
//  SpaceMembersView.swift
//  NoteSpace
//
//  Created by User on 2026-02-19.
//

import SwiftUI

struct SpaceMembersView: View {
    let space: Space
    @EnvironmentObject private var dataManager: DataManager
    @Environment(\.dismiss) var dismiss
    @State private var members: [User] = []
    @State private var showingAlert = false
    @State private var alertMessage = ""
    @State private var selectedMember: User?
    
    var body: some View {
        NavigationView {
            List {
                ForEach(members) { member in
                    HStack {
                        VStack(alignment: .leading) {
                            Text(member.username)
                                .font(.headline)
                            Text(member.email)
                                .font(.caption)
                                .foregroundColor(.gray)
                        }
                        
                        Spacer()
                        
                        // Показываем роль пользователя
                        if member.id == space.creatorId {
                            Label("Creator", systemImage: "crown.fill")
                                .font(.caption)
                                .foregroundColor(.yellow)
                        } else if space.adminIds.contains(member.id) {
                            Label("Admin", systemImage: "shield.fill")
                                .font(.caption)
                                .foregroundColor(.blue)
                        }
                        
                        // Кнопка действий (только для создателя или админа)
                        if canManageMember(member) {
                            Menu {
                                if space.creatorId == dataManager.currentUser?.id {
                                    // Создатель может назначать/снимать админов
                                    if !space.adminIds.contains(member.id) {
                                        Button(action: { makeAdmin(member) }) {
                                            Label("Make Admin", systemImage: "shield")
                                        }
                                    } else {
                                        Button(action: { removeAdmin(member) }) {
                                            Label("Remove Admin", systemImage: "shield.slash")
                                        }
                                    }
                                }
                                
                                // Кнопка удаления (для создателя и админов)
                                if member.id != space.creatorId {
                                    Button(role: .destructive, action: { selectedMember = member }) {
                                        Label("Remove from Space", systemImage: "person.fill.xmark")
                                    }
                                }
                            } label: {
                                Image(systemName: "ellipsis.circle")
                                    .foregroundColor(.blue)
                            }
                        }
                    }
                }
            }
            .navigationTitle("Members (\(members.count))")
            .navigationBarItems(trailing: Button("Done") { dismiss() })
            .onAppear {
                loadMembers()
            }
            .alert("Remove Member", isPresented: $showingAlert) {
                Button("Cancel", role: .cancel) { }
                Button("Remove", role: .destructive) {
                    if let member = selectedMember {
                        removeMember(member)
                    }
                }
            } message: {
                if let member = selectedMember {
                    Text("Are you sure you want to remove \(member.username) from this space?")
                }
            }
        }
    }
    
    private func loadMembers() {
        members = dataManager.getSpaceMembers(spaceId: space.id)
    }
    
    private func canManageMember(_ member: User) -> Bool {
        guard let currentUserId = dataManager.currentUser?.id else { return false }
        
        // Нельзя управлять самим собой (кроме выхода)
        if member.id == currentUserId {
            return false
        }
        
        // Создатель может управлять всеми
        if space.creatorId == currentUserId {
            return true
        }
        
        // Админ может управлять обычными участниками
        if space.adminIds.contains(currentUserId) && !space.adminIds.contains(member.id) && member.id != space.creatorId {
            return true
        }
        
        return false
    }
    
    private func makeAdmin(_ member: User) {
        if dataManager.makeAdmin(spaceId: space.id, memberId: member.id) {
            loadMembers()
        }
    }
    
    private func removeAdmin(_ member: User) {
        if dataManager.removeAdmin(spaceId: space.id, memberId: member.id) {
            loadMembers()
        }
    }
    
    private func removeMember(_ member: User) {
        if dataManager.removeMemberFromSpace(spaceId: space.id, memberId: member.id) {
            loadMembers()
        }
    }
}
