//
//  JoinSpaceView.swift
//  NoteSpace
//
//  Created by User on 2026-02-19.
//

import SwiftUI

struct JoinSpaceView: View {
    @Environment(\.dismiss) var dismiss
    @EnvironmentObject private var dataManager: DataManager
    
    @State private var inviteCode = ""
    @State private var showError = false
    
    var body: some View {
        NavigationView {
            VStack(spacing: 30) {
                TextField("Enter Invite Code", text: $inviteCode)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .padding()
                    .autocapitalization(.allCharacters)
                
                Button(action: joinSpace) {
                    Text("Join Space")
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(Color.blue)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                }
                .padding(.horizontal)
                
                Text("Or scan QR code")
                    .foregroundColor(.gray)
                
                Button(action: scanQRCode) {
                    Image(systemName: "qrcode.viewfinder")
                        .font(.system(size: 50))
                        .foregroundColor(.blue)
                }
                
                Spacer()
            }
            .navigationTitle("Join Space")
            .navigationBarItems(trailing: Button("Close") { dismiss() })
            .alert("Invalid Code", isPresented: $showError) {
                Button("OK", role: .cancel) { }
            }
        }
    }
    
    private func joinSpace() {
        if let userId = dataManager.currentUser?.id {
            if dataManager.joinSpace(inviteCode: inviteCode.uppercased(), userId: userId) {
                dismiss()
            } else {
                showError = true
            }
        }
    }
    
    private func scanQRCode() {
        // QR code scanning implementation would go here
        // For simplicity, we'll just show an alert
        showError = true
    }
}
