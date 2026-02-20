//
//  SpaceDetailView.swift
//  NoteSpace
//
//  Created by User on 2026-02-19.
//

import SwiftUI

struct SpaceDetailView: View {
    let space: Space
    @EnvironmentObject private var dataManager: DataManager
    @State private var showingAddNote = false
    @State private var showingInviteOptions = false
    @State private var showingMembers = false
    @State private var showingLeaveAlert = false
    
    var spaceNotes: [Note] {
        dataManager.notes.filter { $0.spaceId == space.id }
    }
    
    var canManageSpace: Bool {
        guard let userId = dataManager.currentUser?.id else { return false }
        return space.creatorId == userId || space.adminIds.contains(userId)
    }
    
    var body: some View {
        VStack {
            if spaceNotes.isEmpty {
                VStack(spacing: 20) {
                    Image(systemName: "note.text")
                        .font(.system(size: 60))
                        .foregroundColor(.gray)
                    Text("No notes yet")
                        .font(.headline)
                        .foregroundColor(.gray)
                    Text("Tap + to create your first note")
                        .font(.subheadline)
                        .foregroundColor(.gray)
                }
                .frame(maxWidth: .infinity, maxHeight: .infinity)
            } else {
                List {
                    ForEach(spaceNotes) { note in
                        NavigationLink(destination: NoteDetailView(note: note)) {
                            VStack(alignment: .leading, spacing: 8) {
                                Text(note.title)
                                    .font(.headline)
                                Text(note.content)
                                    .font(.subheadline)
                                    .lineLimit(2)
                                    .foregroundColor(.gray)
                                HStack {
                                    Label(note.authorName, systemImage: "person.circle")
                                    Spacer()
                                    Label(note.updatedAt.formatted(date: .abbreviated, time: .shortened),
                                          systemImage: "calendar")
                                }
                                .font(.caption2)
                                .foregroundColor(.blue)
                            }
                            .padding(.vertical, 8)
                        }
                    }
                    .onDelete { indexSet in
                        if canManageSpace {
                            for index in indexSet {
                                let note = spaceNotes[index]
                                dataManager.deleteNote(noteId: note.id, spaceId: space.id)
                            }
                        }
                    }
                }
            }
        }
        .navigationTitle(space.name)
        .toolbar {
            ToolbarItem(placement: .navigationBarTrailing) {
                HStack {
                    // Информация о пространстве
                    Menu {
                        Text("Members: \(space.memberIds.count)")
                        Text("Invite Code: \(space.inviteCode)")
                        Divider()
                        
                        Button(action: { showingMembers = true }) {
                            Label("View Members", systemImage: "person.2")
                        }
                        
                        if canManageSpace {
                            Button(action: { showingInviteOptions = true }) {
                                Label("Invite People", systemImage: "person.badge.plus")
                            }
                        }
                        
                        if space.creatorId != dataManager.currentUser?.id {
                            Button(role: .destructive, action: { showingLeaveAlert = true }) {
                                Label("Leave Space", systemImage: "arrow.right.square")
                            }
                        }
                    } label: {
                        Image(systemName: "info.circle")
                    }
                    
                    // Добавление заметки
                    Button(action: { showingAddNote = true }) {
                        Image(systemName: "plus")
                    }
                }
            }
        }
        .sheet(isPresented: $showingAddNote) {
            AddNoteView(space: space)
        }
        .sheet(isPresented: $showingInviteOptions) {
            InviteView(space: space)
        }
        .sheet(isPresented: $showingMembers) {
            SpaceMembersView(space: space)
        }
        .alert("Leave Space", isPresented: $showingLeaveAlert) {
            Button("Cancel", role: .cancel) { }
            Button("Leave", role: .destructive) {
                if let userId = dataManager.currentUser?.id {
                    _ = dataManager.leaveSpace(spaceId: space.id, userId: userId)
                }
            }
        } message: {
            Text("Are you sure you want to leave this space? You'll lose access to all notes.")
        }
    }
}
