//
//  SpacesView.swift
//  NoteSpace
//
//  Created by User on 2026-02-19.
//

import SwiftUI

struct SpacesView: View {
    @EnvironmentObject private var dataManager: DataManager
    @State private var showingCreateSpace = false
    @State private var showingJoinSpace = false
    
    var body: some View {
        NavigationView {
            VStack {
                if dataManager.spaces.isEmpty {
                    VStack(spacing: 20) {
                        Image(systemName: "rectangle.3.group")
                            .font(.system(size: 60))
                            .foregroundColor(.gray)
                        Text("No spaces yet")
                            .font(.headline)
                            .foregroundColor(.gray)
                        Text("Create your first space or join one")
                            .font(.subheadline)
                            .foregroundColor(.gray)
                        
                        HStack(spacing: 20) {
                            Button(action: { showingCreateSpace = true }) {
                                Label("Create", systemImage: "plus.circle.fill")
                                    .padding()
                                    .background(Color.blue)
                                    .foregroundColor(.white)
                                    .cornerRadius(10)
                            }
                            
                            Button(action: { showingJoinSpace = true }) {
                                Label("Join", systemImage: "qrcode")
                                    .padding()
                                    .background(Color.green)
                                    .foregroundColor(.white)
                                    .cornerRadius(10)
                            }
                        }
                        .padding(.top)
                    }
                } else {
                    List {
                        ForEach(dataManager.spaces) { space in
                            NavigationLink(destination: SpaceDetailView(space: space)) {
                                VStack(alignment: .leading, spacing: 8) {
                                    HStack {
                                        Text(space.name)
                                            .font(.headline)
                                        Spacer()
                                        if space.creatorId == dataManager.currentUser?.id {
                                            Label("Creator", systemImage: "crown.fill")
                                                .font(.caption)
                                                .foregroundColor(.yellow)
                                        } else if space.adminIds.contains(dataManager.currentUser?.id ?? "") {
                                            Label("Admin", systemImage: "shield.fill")
                                                .font(.caption)
                                                .foregroundColor(.blue)
                                        }
                                    }
                                    
                                    Text(space.description)
                                        .font(.subheadline)
                                        .foregroundColor(.gray)
                                    
                                    HStack {
                                        Label("\(space.memberIds.count)", systemImage: "person.2")
                                        Spacer()
                                        Label("\(space.noteIds.count)", systemImage: "note.text")
                                    }
                                    .font(.caption)
                                    .foregroundColor(.blue)
                                }
                                .padding(.vertical, 8)
                            }
                        }
                    }
                }
            }
            .navigationTitle("My Spaces")
            .toolbar {
                if !dataManager.spaces.isEmpty {
                    ToolbarItem(placement: .navigationBarTrailing) {
                        Menu {
                            Button(action: { showingCreateSpace = true }) {
                                Label("Create Space", systemImage: "plus")
                            }
                            Button(action: { showingJoinSpace = true }) {
                                Label("Join Space", systemImage: "qrcode")
                            }
                        } label: {
                            Image(systemName: "plus")
                        }
                    }
                }
            }
            .sheet(isPresented: $showingCreateSpace) {
                CreateSpaceView()
            }
            .sheet(isPresented: $showingJoinSpace) {
                JoinSpaceView()
            }
        }
    }
}
